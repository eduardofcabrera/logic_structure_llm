

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c a)
(on d e)
(on e b)
(clear c)
(clear d)
)
(:goal
(and
(on b e)
(on d c)
(on e a))
)
)


