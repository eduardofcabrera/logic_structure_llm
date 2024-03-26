

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(ontable c)
(on d e)
(on e a)
(clear c)
(clear d)
)
(:goal
(and
(on b c)
(on c a)
(on e b))
)
)


