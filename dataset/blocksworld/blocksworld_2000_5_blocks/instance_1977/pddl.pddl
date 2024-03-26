

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c d)
(on d e)
(ontable e)
(clear b)
(clear c)
)
(:goal
(and
(on a c)
(on d a)
(on e b))
)
)


