

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(ontable c)
(on d e)
(on e b)
(clear a)
(clear c)
(clear d)
)
(:goal
(and
(on b c)
(on c a)
(on d e)
(on e b))
)
)


