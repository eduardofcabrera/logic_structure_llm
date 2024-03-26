

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b d)
(on c e)
(ontable d)
(ontable e)
(clear a)
(clear b)
)
(:goal
(and
(on b a)
(on c d)
(on d e)
(on e b))
)
)


