

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b d)
(ontable c)
(ontable d)
(on e b)
(clear a)
(clear c)
)
(:goal
(and
(on a b)
(on c a)
(on e d))
)
)


